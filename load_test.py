import json
import threading
import time
import urllib.request
from statistics import mean, median


DEVICE_URL = "http://localhost:8000/devices/load_test_device/data"
ANALYTICS_URL = "http://localhost:8000/devices/load_test_device/analytics"
PAYLOAD = json.dumps({"x": 1.5, "y": 2.3, "z": 0.8}).encode()
HEADERS = {"Content-Type": "application/json"}

results = []
lock = threading.Lock()


def send_request():
    start = time.time()
    try:
        req = urllib.request.Request(DEVICE_URL, data=PAYLOAD, headers=HEADERS, method="POST")
        with urllib.request.urlopen(req, timeout=5) as r:
            r.read()
            elapsed = (time.time() - start) * 1000
            with lock:
                results.append({"status": r.status, "ms": elapsed})
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        with lock:
            results.append({"status": 0, "ms": elapsed, "error": str(e)})


def run_load_test(total=200, workers=10):
    print(f"Нагрузочный тест: {total} запросов, {workers} потоков")
    print("-" * 50)

    threads = [threading.Thread(target=send_request) for _ in range(total)]
    start_total = time.time()

    for i in range(0, total, workers):
        batch = threads[i:i + workers]
        for t in batch:
            t.start()
        for t in batch:
            t.join()

    total_time = time.time() - start_total

    success = [r for r in results if r["status"] == 201]
    failed = [r for r in results if r["status"] != 201]
    latencies = [r["ms"] for r in success]

    print(f"Всего запросов:    {total}")
    print(f"Успешных (201):    {len(success)}")
    print(f"Ошибок:            {len(failed)}")
    print(f"Общее время:       {total_time:.2f} сек")
    print(f"Запросов/сек:      {total / total_time:.1f} RPS")
    if latencies:
        print(f"Задержка (мс):")
        print(f"  Среднее:         {mean(latencies):.1f}")
        print(f"  Медиана:         {median(latencies):.1f}")
        print(f"  Минимум:         {min(latencies):.1f}")
        print(f"  Максимум:        {max(latencies):.1f}")

    print("-" * 50)
    print("\nТест эндпоинта аналитики:")
    start = time.time()
    req = urllib.request.Request(ANALYTICS_URL, method="GET")
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    print(f"  Время ответа: {(time.time()-start)*1000:.1f} мс")
    print(f"  Записей в БД (count): {data['x']['count']}")


if __name__ == "__main__":
    run_load_test(total=200, workers=10)
