import mongoose from 'mongoose';

const { Schema, model } = mongoose;

const userSchema = new Schema({
  email: { type: String, required: true, unique: true, lowercase: true, trim: true },
  passwordHash: { type: String, required: true },
  displayName: { type: String },
  createdAt: { type: Date, default: () => new Date() },
  isVerified: { type: Boolean, default: false }
});

export default model('User', userSchema);
