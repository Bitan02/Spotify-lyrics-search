/**
 * MongoDB Schema for Search History
 */
const mongoose = require('mongoose');

const searchHistorySchema = new mongoose.Schema({
  lyrics: {
    type: String,
    required: true,
    trim: true
  },
  song: {
    type: String,
    required: true,
    trim: true
  },
  artist: {
    type: String,
    required: true,
    trim: true
  },
  confidence: {
    type: Number,
    required: true,
    min: 0,
    max: 1
  },
  createdAt: {
    type: Date,
    default: Date.now,
    index: true
  }
}, {
  timestamps: true
});

// Index for faster queries
searchHistorySchema.index({ createdAt: -1 });
searchHistorySchema.index({ song: 1, artist: 1 });

module.exports = mongoose.model('SearchHistory', searchHistorySchema);

