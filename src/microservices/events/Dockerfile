# Этап 1: Сборка (Build)
# Используем Maven с Temurin JDK 17
FROM maven:3.8.5-eclipse-temurin-17 AS build
WORKDIR /app

COPY pom.xml .
RUN mvn dependency:go-offline

COPY src ./src
RUN mvn clean package -DskipTests

# Этап 2: Запуск (Runtime)
# Используем легковесный образ Eclipse Temurin JDK 17
FROM eclipse-temurin:17-jdk-alpine
WORKDIR /app

COPY --from=build /app/target/*.jar app.jar

EXPOSE 8082

ENTRYPOINT ["java", "-jar", "app.jar"]
