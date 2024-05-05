from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
    "mongodb+srv://db_name:password_from_db@cluster_name.unao38c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db = client.book
try:
    # Введення потрібних значень у бд
    result_many = db.cats.insert_many(
        [

            {
                "name": "barsik",
                "age": 3,
                "features": ["ходить в капці", "дає себе гладити", "рудий"],
            },

            {
                "name": "Lama",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Liza",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
        ]
    )
    print(result_many.inserted_ids)
except Exception as e:
    print(e)


# Виведення усіх звірів які є в бд
def all_pets_in_book():
    try:
        result = db.cats.find()
        pets = []
        for doc in result:
            pets.append(doc)

        return pets
    except Exception as e:
        print(e)


# Виведення тільки одного звіра за іменем
def show_one_of_pets(pet_name):
    try:
        result = db.cats.find({"name": pet_name})
        pet = []
        for re in result:
            pet.append(re)

        return pet
    except Exception as e:
        print(e)


# Оновлення за іменем звіра його вік
def update_pet_name(pet_name, pet_age):
    try:
        db.cats.update_one({"name": pet_name}, {"$set": {"age": pet_age}})
        return "Updating was success!"

    except Exception as e:
        print(e)


# Оновлення за іменем звіра його опис(функції які він там виконує)
def add_feauters_for_cat(cat_name, new_feauters):
    try:
        db.cats.update_one({"name": cat_name}, {"$set": {"features": new_feauters}}, upsert=True)
        return "Update was success"
    except Exception as e:
        print(e)


# видалення одного звіра за іменем(навіть якщо є повторення)
def delete_one_pet(pet_name):
    try:
        result = db.cats.delete_one({"name": pet_name})
        return "Delete pet was success!"

    except Exception as e:
        print(e)


# видалення усіх звірів за іменем і усі повторення також видаляються
def delete_all_pets_with_name(pet):
    try:
        result = db.cats.delete_many({"name": pet})
        return "Delete pets was success!"

    except Exception as e:
        print(e)


# Видаляємо всі документи з вказаної колекції
def delete_all_records_from_collection():
    try:
        db.cats.delete_many({})
        return f"Deleted all records succesfully."
    except Exception as e:
        print(e)


result = db.cats.find_one({"name": "Liza"})
print(result)

print(all_pets_in_book())

res = show_one_of_pets("Lama")
print(res)

pet_name = input("Enter a pet_name: ")
pet_age = input("Enter a wish cat age: ")
result = update_pet_name(pet_name, pet_age)
print(result)

cat_name = input("Enter a cat name: ")
new_feauters = input("Enter a new features: ")

result = add_feauters_for_cat(cat_name, new_feauters)
print(result)

result = db.cats.find_one({"name": "Liza"})
print(result)



res = input("Enter a pet name: ")
d_p = delete_one_pet(res)
print(d_p)
print(db.cats.find_one({"name": "Liza"}))



res = input("Enter a name pet for delete all pets with this name: ")
result = delete_all_pets_with_name(res)
print(result)
print(db.cats.find_one({"name": "Lama"}))



result = delete_all_records_from_collection()
print(result)
