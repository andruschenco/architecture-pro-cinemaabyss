package main.java.com.cinemaabyss.events;

// Файл: src/main/java/CinemaEvent.java
public class CinemaEvent {
    private String type;
    private String payload;

    public CinemaEvent() {} // Пустой конструктор для Jackson

    public CinemaEvent(String type, String payload) {
        this.type = type;
        this.payload = payload;
    }

    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public String getPayload() { return payload; }
    public void setPayload(String payload) { this.payload = payload; }
}
