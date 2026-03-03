package main.java.com.cinemaabyss.events;

// Файл: src/main/java/EventConsumer.java
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class EventConsumer {
    private static final Logger log = LoggerFactory.getLogger(EventConsumer.class);

    @KafkaListener(topics = {"user-events", "payment-events", "movie-events"}, groupId = "cinema-group")
    public void consume(CinemaEvent event) {
        log.info("Received event: Type [{}], Data: {}", event.getType(), event.getPayload());
    }
}
