### Шаг 1. Полная очистка Helm-релиза и данных
Удалим все поды, PVC (PersistentVolumeClaims) и сам релиз.

#### 1.1 Удалим Helm-релиз
```bash
  helm uninstall cinemaabyss --namespace cinemaabyss
```
#### 1.2 Проверим, что PVC удалилены
```bash
  kubectl -n cinemaabyss get pvc
```
Если PVC остались в статусе Terminating, удалите их принудительно:
```bash
  kubectl -n cinemaabyss delete pvc --all --namespace cinemaabyss
```
#### 1.3 Удалим namespace (если нужно реально "в ноль")
```bash
  kubectl delete namespace cinemaabyss
```
После этого можно создать namespace заново позже командой helm install (она создаст его автоматически с флагом --create-namespace).

### Шаг 2. Чистая установка Helm-чарта
```bash
  helm install cinemaabyss ./IdeaProjects/architecture-pro-cinemaabyss/src/kubernetes/helm --namespace cinemaabyss --create-namespace
```    
### Шаг 3. Мониторинг запуска
Следим за подами
```bash
  kubectl -n cinemaabyss get pods -w
```

### Шаг 4. Проверка тестов "убедись, что тесты в kubernetes проходят". 
```bash
  npm run test:kubernetes
```
#### # Результат такой
   ```bash
┌─────────────────────────┬────────────────────┬───────────────────┐
│                         │           executed │            failed │
├─────────────────────────┼────────────────────┼───────────────────┤
│              iterations │                  1 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│                requests │                 22 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│            test-scripts │                 22 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│      prerequest-scripts │                  0 │                 0 │
├─────────────────────────┼────────────────────┼───────────────────┤
│              assertions │                 42 │                 0 │
├─────────────────────────┴────────────────────┴───────────────────┤
│ total run duration: 4.7s                                         │
├──────────────────────────────────────────────────────────────────┤
│ total data received: 5.9kB (approx)                              │
├──────────────────────────────────────────────────────────────────┤
│ average response time: 84ms [min: 8ms, max: 1091ms, s.d.: 226ms] │
└──────────────────────────────────────────────────────────────────┘
Newman run completed!
Total requests: 22
Failed requests: 0
Total assertions: 42
Failed assertions: 0
```

#### Вариант проверки health - следить за логами proxy-service в реальном времени
```bash
  kubectl -n cinemaabyss logs -f -l app=proxy-service
```
#### Вариант проверки health - в отчете 
 [junit-report-kubernetes-2026-03-03T22-18-40.882Z.xml](junit-report-kubernetes-2026-03-03T22-18-40.882Z.xml)

---