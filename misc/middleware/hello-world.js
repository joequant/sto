const express = require('express')
const readlineSync = require('readline-sync')
const http = require('http')
const app = express()
const port = 3000
const server= http.createServer(app);


app.get('/', (req, res) => res.send('Hello World!'))
server.listen(port)
console.log('running listen')
s
