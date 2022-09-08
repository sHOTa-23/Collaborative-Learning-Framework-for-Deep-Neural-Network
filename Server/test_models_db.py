from ModelAccuraciesRepository import ModelAccuraciesRepository

db = ModelAccuraciesRepository("mongodb+srv://doadmin:g12k79jU8L3y0u5t@db-mongodb-nyc3-12601-daeda50b.mongo.ondigitalocean.com/admin?authSource=admin&replicaSet=db-mongodb-nyc3-12601&tls=true")

print(db.get_clients_accuracies())