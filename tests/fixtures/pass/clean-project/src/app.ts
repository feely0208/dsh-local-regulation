import express from 'express';
import { verifyMemberFace } from './face/verify.js';

const app = express();
app.use(express.json());

app.get('/', (_req, res) => {
  res.send('星链会员平台');
});

app.post('/gate/verify', async (req, res) => {
  const result = await verifyMemberFace(req.body.frame);
  res.json(result);
});

app.listen(8080, () => {
  console.log('member web listening on 8080');
});
