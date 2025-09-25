import { Router } from 'express';
import Joi from 'joi';
import { db } from '../config/database.js';
import { requireAuth } from '../middleware/auth.js';

const router = Router();

const profileSchema = Joi.object({
  height_cm: Joi.number().min(50).max(300),
  weight_kg: Joi.number().min(20).max(500),
  age: Joi.number().min(5).max(120),
  gender: Joi.string().valid('male', 'female', 'other'),
  ethnicity: Joi.string().max(120),
  diet_restrictions: Joi.array().items(Joi.string()).default([])
});

router.get('/me', requireAuth, async (req, res, next) => {
  try {
    const user = await db('users').where({ id: req.user.id }).first();
    if (!user) return res.status(404).json({ error: 'Not found' });
    res.json({
      id: user.id,
      email: user.email,
      name: user.name,
      height_cm: user.height_cm,
      weight_kg: user.weight_kg,
      age: user.age,
      gender: user.gender,
      ethnicity: user.ethnicity,
      diet_restrictions: user.diet_restrictions || []
    });
  } catch (err) {
    next(err);
  }
});

router.put('/me', requireAuth, async (req, res, next) => {
  try {
    const { value, error } = profileSchema.validate(req.body);
    if (error) return res.status(400).json({ error: error.message });
    const [updated] = await db('users')
      .where({ id: req.user.id })
      .update({ ...value }, ['id', 'email', 'name', 'height_cm', 'weight_kg', 'age', 'gender', 'ethnicity', 'diet_restrictions']);
    res.json(updated);
  } catch (err) {
    next(err);
  }
});

export default router;
