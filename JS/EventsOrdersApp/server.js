require('dotenv').config();
const express = require('express');
const nodemailer = require('nodemailer');
const app = express();
app.use(express.json());
app.use(express.urlencoded({extended: true}));
const port = process.env.PORT || 3001;
const cors = require('cors');



app.use(cors());

function sendEmail(order) {
    console.log(order);
    return new Promise((resolve, reject) => {
        
        
        
        
        const transporter = nodemailer.createTransport({
            service: 'gmail',
            auth: {
                user: process.env.NODEMAILER_USER, 
                pass: process.env.NODEMAILER_PASS
            }
        });

        const mailOptions = {
            from: '"Averys Events" <events.averys@gmail.com>',
            to: order.customerEmail,
            cc: "adam.willis@averys.com",//order.email,
            replyTo: "events@averys.com",
            subject: `Order Submitted - ${order.name}`,
            
            html: `<p style="font-family: Arial, sans-serif; font-size: 16px; margin-bottom: 20px;">
  Thank you for your order! See below your summary:
</p>

<h1 style="font-weight: bold; text-align: center; background-color: #fff3cd; color: #856404; padding: 12px; border: 1px solid #ffeeba; border-radius: 6px; font-size: 18px;">
  **PLEASE NOTE YOUR ORDER IS NOT CONFIRMED UNTIL PAYMENT IS MADE AT THE ORDERS TABLE**<br>
  PLEASE SEND ANY ORDER QUERIES TO events@averys.com
</h1>

<h2 style="font-family: Arial, sans-serif; font-size: 18px; margin-top: 24px; border-bottom: 2px solid #ccc; padding-bottom: 6px;">
  Customer Details:
</h2>

<table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-family: Arial, sans-serif; font-size: 16px;">
  <tr>
    <td style="border: 1px solid #ccc; padding: 8px;"><strong>Name:</strong></td>
    <td style="border: 1px solid #ccc; padding: 8px;">${order.name}</td>
  </tr>
  <tr>
    <td style="border: 1px solid #ccc; padding: 8px;"><strong>Phone:</strong></td>
    <td style="border: 1px solid #ccc; padding: 8px;">${order.phone}</td>
  </tr>
  <tr>
    <td style="border: 1px solid #ccc; padding: 8px;"><strong>Customers Email:</strong></td>
    <td style="border: 1px solid #ccc; padding: 8px;">${order.customerEmail}</td>
  </tr>
</table>

<h2 style="font-family: Arial, sans-serif; font-size: 18px; margin-top: 24px; border-bottom: 2px solid #ccc; padding-bottom: 6px;">
  Order Details:
</h2>

<p style="font-family: Arial, sans-serif; font-size: 16px;"><strong>Bottles in Basket:</strong> ${order.bottlesInBasket}</p>
<p style="font-family: Arial, sans-serif; font-size: 16px;"><strong>Order Total:</strong> £${order.orderTotal}</p>

<table style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; font-size: 16px;">
  <tr style="background-color: #0F3B3E; color: #FFFFE6;">
    <th style="border: 1px solid #ccc; padding: 8px;">Table</th>
    <th style="border: 1px solid #ccc; padding: 8px;">Wine Number</th>
    <th style="border: 1px solid #ccc; padding: 8px;">SKU</th>
    <th style="border: 1px solid #ccc; padding: 8px;">Wine</th>
    <th style="border: 1px solid #ccc; padding: 8px;">Price</th>
    <th style="border: 1px solid #ccc; padding: 8px;">Qty</th>
  </tr>
  ${order.basket.map(item => `
    <tr>
      <td style="border: 1px solid #ccc; padding: 8px;">${item.Table}</td>
      <td style="border: 1px solid #ccc; padding: 8px;">${item.Number}</td>
      <td style="border: 1px solid #ccc; padding: 8px;">${item.SKU}</td>
      <td style="border: 1px solid #ccc; padding: 8px;">${item.Wine}</td>
      <td style="border: 1px solid #ccc; padding: 8px;">£${Number(order.bottlesInBasket) >= 6 ? item['6Price'] : item['1Price']}</td>
      <td style="border: 1px solid #ccc; padding: 8px;">${item.Qty}</td>
    </tr>
  `).join('')}
</table>`
        };
        console.log("Sending Mail options: ", mailOptions);
        transporter.sendMail(mailOptions, (error, info) => {
            if (error) {
                console.log("Error while sending email: ", error);
                return reject('Error while sending email: ' + error);
            }
            console.log("Email sent: ", info.response);
            return resolve('Email sent successfully: ' + info.response);
        });
    });
}

app.get('/', (req, res) => {
    res.send('Email Service is running');
});



// app.get('/send', (req, res) => {
//     console.log("Received request to send email");
//     sendEmail()
//         .then(message => res.send(message))
//         .catch(error => res.status(500).send(error));
// });

app.post('/', (req, res) => {
    
    sendEmail(req.body)
        .then(message => res.send(message))
        .catch(error => res.status(500).send(error));
      
})

app.listen(port, () => {
    console.log(`Server running http://localhost:${port}`);
});
