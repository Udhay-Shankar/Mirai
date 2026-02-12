import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import { MONGODB_URI, PORT, CORS_ORIGINS } from './config.js';
import authRoutes from './routes/auth.js';
import scraperRoutes from './routes/scraper.js';

const app = express();

// Middleware
app.use(cors({
  origin: CORS_ORIGINS.length > 0 ? CORS_ORIGINS : '*',
  credentials: true
}));
app.use(express.json());

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/scrape', scraperRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Connect to MongoDB and start server
async function start() {
  try {
    await mongoose.connect(MONGODB_URI);
    console.log('✅ Connected to MongoDB Atlas');
    
    app.listen(PORT, () => {
      console.log(`🚀 Server running on http://localhost:${PORT}`);
      console.log(`📝 API endpoints:`);
      console.log(`   POST   /api/auth/signup`);
      console.log(`   POST   /api/auth/login`);
      console.log(`   GET    /api/auth/me (protected)`);
    });
  } catch (error) {
    console.error('❌ Failed to start server:', error);
    process.exit(1);
  }
}

start();
