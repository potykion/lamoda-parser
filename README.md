# lamoda-parser

Парсер Lamoda

# Как пользоваться

Собираем и запускаем Docker-образ:

```
docker build -t myimage .
docker run -d --name mycontainer -p 80:80 myimage
```

Передаем ссылку на шмотку, например [такую](https://www.lamoda.ru/p/he002emklgv2/clothes-hebymango-futbolka/) в urlencoded-виде:

```
http://127.0.0.1/?url=https%3A%2F%2Fwww.lamoda.ru%2Fp%2Fhe002emklgv2%2Fclothes-hebymango-futbolka%2F
```

Получаем JSON-инфу по шмотке:

```
{
    "title": "CHERLO",
    "brand": "Mango Man",
    "type": "Футболка",
    "images": [
        "https://a.lmcdn.ru/img600x866/H/E/HE002EMKLGV2_11830317_2_v1.jpg",
        "https://a.lmcdn.ru/img600x866/H/E/HE002EMKLGV2_11830318_3_v1.jpg",
        "https://a.lmcdn.ru/img600x866/H/E/HE002EMKLGV2_11830316_1_v1.jpg"
    ]
}
```