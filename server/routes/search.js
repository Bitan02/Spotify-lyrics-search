/**
 * Search Routes
 * Handles lyric search requests and communicates with ML service
 */
const express = require('express');
const router = express.Router();
const axios = require('axios');
const SearchHistory = require('../models/SearchHistory');

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:8000';

/**
 * POST /api/search
 * Search for song by lyrics
 */
router.post('/search', async (req, res) => {
  try {
    const { lyrics } = req.body;

    // Validate input
    if (!lyrics || typeof lyrics !== 'string' || lyrics.trim().length === 0) {
      return res.status(400).json({
        error: 'Lyrics input is required and must be a non-empty string'
      });
    }

    // Call ML service
    let mlResponse;
    try {
      mlResponse = await axios.post(`${ML_SERVICE_URL}/predict`, {
        lyrics: lyrics.trim()
      });
    } catch (error) {
      if (error.response) {
        // ML service returned an error
        return res.status(error.response.status).json({
          error: error.response.data.detail || 'ML service error'
        });
      } else if (error.request) {
        // Request was made but no response received
        return res.status(503).json({
          error: 'ML service is unavailable. Please ensure it is running.'
        });
      } else {
        // Error in setting up request
        return res.status(500).json({
          error: 'Error calling ML service'
        });
      }
    }

    const { song, artist, confidence } = mlResponse.data;

    // Save to database
    const searchRecord = new SearchHistory({
      lyrics: lyrics.trim(),
      song,
      artist,
      confidence
    });

    await searchRecord.save();

    // Return result
    res.json({
      success: true,
      data: {
        song,
        artist,
        confidence,
        id: searchRecord._id
      }
    });
  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
});

module.exports = router;

