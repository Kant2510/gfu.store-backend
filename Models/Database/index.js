const { MongoClient } = require('mongodb')

class Database {
    constructor(url, dbName) {
        this.url = url

        this.dbName = dbName

        this.client = new MongoClient(this.url)

        this.Database = null
    }
    async connect() {
        try {
            console.log('Waiting for connect to database...')
            await this.client.connect()
            console.log('Connected correctly to database!')

            this.Database = this.client.db(this.dbName)

        } catch (err) {
            console.log(err.stack)
        }

        // finally {
        //     await client.close()
        // }
    }
    async add(name, data) {
        if (this.Database !== null) {

            const collection = this.Database.collection(name)

            return await collection.insertOne(data)
        }
    }
    async find(name, data) {
        if (this.Database !== null) {

            const collection = this.Database.collection(name)

            return await collection.findOne(data)
        }
    }
    async remove(name, data) {
        if (this.Database !== null) {

            const collection = this.Database.collection(name)

            return await collection.deleteOne(name, data)
        }
    }
    async find_push(name, data, filter) {
        if (this.Database !== null) {

            const collection = this.Database.collection(name)

            await collection.findOneAndUpdate(
                filter,
                { $push: { products: data } },
                { upsert: true },
                function (err, user) {
                    //after mongodb is done updating, you are receiving the updated file as callback    

                    // now you can send the error or updated file to client
                    if (err)
                        res.send(err);

                    return 'error';
                })
        }
    }

}
module.exports = Database