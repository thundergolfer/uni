use proc_macro2::Span;
use quote::{quote, ToTokens};
use rust_format::{Formatter, PrettyPlease};
use syn::Attribute;
use syn::Meta;
use syn::{parse_macro_input, ItemFn, Lit, ReturnType, Type};

/// Procedural macro that provides easy access (via two generated functions) to
/// the documentation and source code body of a function.
/// Used as part of the benchmarking data export.
#[proc_macro_attribute]
pub fn gen_docs(
    _attr: proc_macro::TokenStream,
    item: proc_macro::TokenStream,
) -> proc_macro::TokenStream {
    // Extract a well-formatted fn body is actually pretty annoying.
    // We must:
    // 1. Remove the doc string comments
    // 2. Remove the fn signature, which is identical for each bench and thus boring boilerplate
    // 3. Format the fn signature-less code, which is hella fiddly.
    // 4. Stripe the surrounding braces from the code block.
    //
    // Only after all those steps do we get the function body un-indented and nicely formatted.
    let input_fn = parse_macro_input!(item as ItemFn);
    // (1) Filter out doc attributes from the fn AST.
    let non_doc_attrs: Vec<&Attribute> = input_fn
        .attrs
        .iter()
        .filter(|attr| !attr.path().is_ident("doc"))
        .collect();
    let func_without_docs = ItemFn {
        attrs: non_doc_attrs.into_iter().cloned().collect(),
        ..input_fn.clone()
    };
    // (2) Remove fn signature it's boring
    let block = func_without_docs.block;
    let input_fn_src = block.to_token_stream().to_string();
    // (3) Annoyingly rust_format can't format just a single code block, so we temporary give this
    //     a fake fn wrapping.
    let mut source = "fn foo() ".to_string();
    source.push_str(&input_fn_src);
    source = PrettyPlease::default().format_str(source).unwrap();
    let source = source
        .strip_prefix("fn foo() ")
        .unwrap()
        .replace("    ", "\t");
    // (4) We now have this:
    //
    // {
    //     BODY
    // }
    //
    // Remove the braces and un-indent.
    let source: String = source
        .split("\n")
        .skip(1)
        .take_while(|x| !x.starts_with("}"))
        .map(|l| l.strip_prefix("\t").unwrap_or(l))
        .collect::<Vec<_>>()
        .join("\n");

    // Create the function which returns fn body source code (with "_src" suffix)
    let fn_name = &input_fn.sig.ident;
    let src_fn_name = syn::Ident::new(&format!("{}_src", fn_name), fn_name.span());
    let src_fn = syn::ItemFn {
        attrs: vec![],
        vis: input_fn.vis.clone(),
        sig: syn::Signature {
            output: ReturnType::Type(
                syn::token::RArrow::default(),
                Box::new(Type::Reference(syn::TypeReference {
                    and_token: syn::token::And::default(),
                    lifetime: Some(syn::Lifetime::new("'static", Span::call_site())),
                    mutability: None,
                    elem: Box::new(Type::Path(syn::TypePath {
                        qself: None,
                        path: syn::Path::from(syn::Ident::new("str", Span::call_site())),
                    })),
                })),
            ),
            inputs: syn::punctuated::Punctuated::new(),
            variadic: None,
            ident: src_fn_name,
            ..input_fn.sig.clone()
        },
        block: Box::new(syn::parse_quote!({
            const SOURCE: &'static str = #source;
            SOURCE
        })),
    };

    // Create the function which returns fn doc string (with "_doc" suffix)
    let doc_fn_name = syn::Ident::new(&format!("{}_doc", fn_name), fn_name.span());
    let doc_string = extract_doc_strings(&input_fn).join("\n");
    let doc_fn = syn::ItemFn {
        attrs: vec![],
        vis: input_fn.vis.clone(),
        sig: syn::Signature {
            output: ReturnType::Type(
                syn::token::RArrow::default(),
                Box::new(Type::Reference(syn::TypeReference {
                    and_token: syn::token::And::default(),
                    lifetime: Some(syn::Lifetime::new("'static", Span::call_site())),
                    mutability: None,
                    elem: Box::new(Type::Path(syn::TypePath {
                        qself: None,
                        path: syn::Path::from(syn::Ident::new("str", Span::call_site())),
                    })),
                })),
            ),
            inputs: syn::punctuated::Punctuated::new(),
            variadic: None,
            ident: doc_fn_name,
            ..input_fn.sig.clone()
        },
        block: Box::new(syn::parse_quote!({
            const DOCS: &'static str = #doc_string;
            DOCS
        })),
    };

    // Generate the output, including both the original and new function
    let output = quote! {
        #input_fn

        #src_fn

        #doc_fn
    };

    output.into()
}

fn extract_doc_strings(item_fn: &ItemFn) -> Vec<String> {
    item_fn
        .attrs
        .iter()
        .filter_map(|attr| {
            if attr.path().is_ident("doc") {
                match &attr.meta {
                    Meta::NameValue(name_value) => match &name_value.value {
                        syn::Expr::Lit(expr_lit) => match &expr_lit.lit {
                            Lit::Str(ls) => Some(ls.value()),
                            _ => None,
                        },
                        _ => None,
                    },
                    _ => None,
                }
            } else {
                None
            }
        })
        .collect()
}
