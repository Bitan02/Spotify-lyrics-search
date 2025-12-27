/**
 * History Routes
 * Handles search history retrieval
 */
const express = require('express');
const router = express.Router();
const SearchHistory = require('../models/SearchHistory');

/**
 * GET /api/history
 * Get search history with pagination
 */
router.get('/history', async (req, res) => {
  try {
    const page = parseInt(req.query.page) || 1;
    const limit = parseInt(req.query.limit) || 20;
    const skip = (page - 1) * limit;

    // Validate pagination parameters
    if (page < 1 || limit < 1 || limit > 100) {
      return res.status(400).json({
        error: 'Invalid pagination parameters. Page must be >= 1, limit must be between 1 and 100.'
      });
    }

    // Get total count for pagination
    const total = await SearchHistory.countDocuments();

    // Get search history (most recent first)
    const history = await SearchHistory.find()
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit)
      .select('-__v') // Exclude version key
      .lean();

    res.json({
      success: true,
      data: history,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    console.error('History retrieval error:', error);
    res.status(500).json({
      error: 'Internal server error',
      message: error.message
    });
  }
});

module.exports = router;

