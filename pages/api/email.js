export default function (req, res) {
  let nodemailer = require("nodemailer");
  require("dotenv").config();
  const PASSWORD = process.env.password;
  const transporter = nodemailer.createTransport({
    port: 465,
    host: "smtp.gmail.com",
    auth: {
      user: "my.damn.poor.soul@gmail.com",
      pass: PASSWORD,
    },
    secure:true,
    tls: {
      rejectUnauthorized: false,
    },
  });
  const mailData = {
    from: "my.damn.poor.soul@gmail.com",
    to: "work.quangviet.1701@gmail.com",
    subject: `Message from your website by ${req.body.name}`,
    text: req.body.message,
    html: `<div>
    <h3 style="">Sender Email: ${req.body.email}</h3>
    <h4>Sender Phone: ${req.body.phone}</h4>
    <p>${req.body.message}</p>
    </div>`,
  };
   transporter.sendMail (mailData, function (err, info) {
    if (err) {
      console.log(err.message);
      
    } else console.log(info.response);
  });
  res.status(200).end();
}
