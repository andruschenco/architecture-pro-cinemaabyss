package main.java.com.cinemaabyss.events;

import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus; // Не забудьте импорт

@RestController
@RequestMapping("/api/events")
public class EventController {

    private final KafkaTemplate<String, CinemaEvent> kafkaTemplate;

    public EventController(KafkaTemplate<String, CinemaEvent> kafkaTemplate) {
        this.kafkaTemplate = kafkaTemplate;
    }

    @PostMapping("/{type}")
    @ResponseStatus(HttpStatus.CREATED) // Это заставит Spring вернуть 201 вместо 200
    public String createEvent(@PathVariable String type, @RequestBody String payload) {
        String topic = type + "-events";
        kafkaTemplate.send(topic, new CinemaEvent(type.toUpperCase(), payload));
        return "{\"status\": \"success\"}";
    }

    @GetMapping("/health")
    public String health() {
        return "{\"status\": true}";
    }
}




