import express from "express";
import axios from "axios";

const app = express()
const port = process.env.PORT || 4080

import dotenv from 'dotenv-safe'
dotenv.config({
    allowEmptyValues: true
})

app.use(express.json()) // 把消息体解析为json
app.use(express.urlencoded({ extended: true })) // for parsing application/x-www-form-urlencoded

// 通过测试
app.get('/demo', async (req, res) => {
    res.status(200).send({ msg: 'scuccess' })
})

app.post('/demo', async (req, res) => {
    // 先发送一个200，表示收到了，避免后端再次发送
    res.status(200).send({ msg: 'scuccess' })

    let { from_uid: fromUid, created_at: createdAt, detail: { content, properties: { content_type: contentDetailType, mentions, name }, content_type: contentType, }, mid, target } = req.body;

    // 发送消息
    await sendMessage(fromUid, `get your message`)

    // 指定关键词
    if (content === 'ping') {
        await sendMessage(fromUid, `pong`)
    }
})

// 请自行模块化
async function sendMessage(fromUid, message) {
    const endpoint = `${process.env.BASE_URL}/api/bot/send_to_user/${fromUid}`
    const apiKey = process.env.BOT_API_KEY
    const response = await axios.post(endpoint, `${message}`, {
        headers: {
            "Content-Type": "text/markdown",
            "x-api-key": apiKey,
            "accept": 'application/json; charset=utf-8',
        },
    })
    // 返回消息id,当前无用
    return response.data
}

app.listen(port, () => {
    console.log(`service working on port ${port}`)
})