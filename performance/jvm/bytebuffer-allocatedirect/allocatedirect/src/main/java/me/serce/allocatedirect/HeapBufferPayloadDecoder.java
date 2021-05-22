package me.serce.allocatedirect;

import io.netty.buffer.ByteBuf;
import io.netty.buffer.Unpooled;
import io.rsocket.Payload;
import io.rsocket.frame.*;
import io.rsocket.frame.decoder.PayloadDecoder;
import io.rsocket.util.DefaultPayload;

import java.nio.ByteBuffer;

public class HeapBufferPayloadDecoder implements PayloadDecoder {

  public static final PayloadDecoder INSTANCE = new HeapBufferPayloadDecoder();

  @Override
  public Payload apply(ByteBuf byteBuf) {
    ByteBuf m;
    ByteBuf d;
    FrameType type = FrameHeaderCodec.frameType(byteBuf);
    switch (type) {
      case REQUEST_FNF:
        d = RequestFireAndForgetFrameCodec.data(byteBuf);
        m = RequestFireAndForgetFrameCodec.metadata(byteBuf);
        break;
      case REQUEST_RESPONSE:
        d = RequestResponseFrameCodec.data(byteBuf);
        m = RequestResponseFrameCodec.metadata(byteBuf);
        break;
      case REQUEST_STREAM:
        d = RequestStreamFrameCodec.data(byteBuf);
        m = RequestStreamFrameCodec.metadata(byteBuf);
        break;
      case REQUEST_CHANNEL:
        d = RequestChannelFrameCodec.data(byteBuf);
        m = RequestChannelFrameCodec.metadata(byteBuf);
        break;
      case NEXT:
      case NEXT_COMPLETE:
        d = PayloadFrameCodec.data(byteBuf);
        m = PayloadFrameCodec.metadata(byteBuf);
        break;
      case METADATA_PUSH:
        d = Unpooled.EMPTY_BUFFER;
        m = MetadataPushFrameCodec.metadata(byteBuf);
        break;
      default:
        throw new IllegalArgumentException("unsupported frame type: " + type);
    }

    ByteBuffer data = ByteBuffer.allocate(d.readableBytes());
    data.put(d.nioBuffer());
    data.flip();

    if (m != null) {
      ByteBuffer metadata = ByteBuffer.allocate(m.readableBytes());
      metadata.put(m.nioBuffer());
      metadata.flip();

      return DefaultPayload.create(data, metadata);
    }

    return DefaultPayload.create(data);
  }
}
