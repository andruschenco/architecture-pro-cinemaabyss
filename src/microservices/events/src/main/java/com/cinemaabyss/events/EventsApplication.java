package main.java.com.cinemaabyss.events;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication // Эта аннотация запускает сканирование контроллеров
public class EventsApplication {
    public static void main(String[] args) {
        SpringApplication.run(EventsApplication.class, args);
    }
}
