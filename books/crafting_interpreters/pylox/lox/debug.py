import chunk as chnk


def disassemble_chunk(chunk: chnk.Chunk, name: str):
    print(f"== {name} ==")

    for b in chunk.code:
        offset = disassemble_instruction(chunk, offset)


def disassemble_instruction(chunk: chnk.Chunk, offset: int) -> int:
    print(chunk.code[offset])
    return offset + 1
