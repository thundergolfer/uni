package me.serce.allocatedirect;

import io.rsocket.RSocket;
import io.rsocket.core.RSocketConnector;
import io.rsocket.core.RSocketServer;
import io.rsocket.frame.decoder.PayloadDecoder;
import io.rsocket.transport.netty.client.TcpClientTransport;
import io.rsocket.transport.netty.server.TcpServerTransport;
import io.rsocket.util.ByteBufPayload;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import reactor.core.publisher.DirectProcessor;
import reactor.core.publisher.Flux;

import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.atomic.AtomicReference;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import static io.rsocket.SocketAcceptor.forRequestChannel;

public class Main {
  private static final Logger logger = LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) throws Exception {
    List<String> argList = Arrays.asList(args);
    var decoder = argList.contains("heap") //
        ? HeapBufferPayloadDecoder.INSTANCE // heap buffer decoder
        : PayloadDecoder.DEFAULT; // default direct buffer decoder
    var sizePattrn = Pattern.compile("size=([0-9]*)");
    var size = -1;
    for (String arg : argList) {
      Matcher matcher;
      if ((matcher = sizePattrn.matcher(arg)).matches()) {
        size = Integer.parseInt(matcher.group(1));
        logger.info("using size {} bytes", size);
      }
    }

    logger.info("starting backend using {} decoder", decoder.getClass().getSimpleName());
    var port = 13131;
    var server = RSocketServer.create(forRequestChannel( //
        payloads -> { //
          return Flux.from(payloads)
              .map(p -> ByteBufPayload.create("ack: " + p.getDataUtf8()));
        })) //
        .payloadDecoder(decoder)
        .bind(TcpServerTransport.create(port))
        .block();
    var client = RSocketConnector.create() //
        .payloadDecoder(decoder)
        .connect(TcpClientTransport.create(port))
        .block();
    Runtime.getRuntime().addShutdownHook(new Thread(() -> {
      logger.info("shutting down");
      client.dispose();
      server.dispose();
    }));

    for (int i = 0; i < 2; i++) {
      launchEchoChannel(client, size);
    }
    Thread.currentThread().join();
  }

  private static void launchEchoChannel(RSocket client, int size) {
    var out = DirectProcessor.<String>create();
    var prev = new AtomicReference<>("init");
    var counter = new AtomicInteger(0);
    client.requestChannel(out.map(ByteBufPayload::create))
        .subscribe( //
            p -> {
              var expected = "ack: " + prev.get();
              if (!Objects.equals(expected, p.getDataUtf8())) {
                throw new RuntimeException("failed, expected: " + expected + ", got " + p.getDataUtf8());
              }
              int nextSize = size > 0 ? size : ThreadLocalRandom.current().nextInt(256, 1024);
              var next = new byte[nextSize];
              ThreadLocalRandom.current().nextBytes(next);
              prev.set(new String(next));
              out.onNext(prev.get());
              if (counter.getAndIncrement() % 50000 == 0) {
                logger.info("processed {} messages", counter.get());
              }
            }, //
            e -> logger.error("error arrived", e), //
            () -> logger.info("completed"));
    out.onNext(prev.get());
  }
}
