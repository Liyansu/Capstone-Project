import { Router } from 'express';
import { requireAuth } from '../middleware/auth.js';

const router = Router();

router.get('/summary', requireAuth, async (req, res) => {
  res.json({ calories_today: 0, compliance: 0 });
});

export default router;
