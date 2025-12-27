import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { searchSong } from '../services/api';

const HomePage = () => {
  const [lyrics, setLyrics] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!lyrics.trim()) {
      setError('Please enter some lyrics');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await searchSong(lyrics);
      
      // Navigate to result page with data
      navigate('/result', {
        state: {
          song: response.data.song,
          artist: response.data.artist,
          confidence: response.data.confidence,
          lyrics: lyrics.trim()
        }
      });
    } catch (err) {
      setError(err.message || 'An error occurred while searching');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="max-w-2xl w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-5xl font-bold text-white mb-4">
            🎵 Spotify Lyric Search
          </h1>
          <p className="text-xl text-blue-200">
            Find songs by entering a snippet of lyrics
          </p>
        </div>

        {/* Search Form */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label 
                htmlFor="lyrics" 
                className="block text-sm font-medium text-white mb-2"
              >
                Enter Lyrics
              </label>
              <textarea
                id="lyrics"
                value={lyrics}
                onChange={(e) => {
                  setLyrics(e.target.value);
                  setError('');
                }}
                placeholder="Type a few lines from a song..."
                className="w-full px-4 py-3 rounded-lg bg-white/90 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white resize-none"
                rows="6"
                disabled={loading}
              />
              <p className="mt-2 text-sm text-blue-200">
                Enter at least a few words from the song you're looking for
              </p>
            </div>

            {error && (
              <div className="bg-red-500/20 border border-red-500/50 rounded-lg p-4">
                <p className="text-red-200 text-sm">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || !lyrics.trim()}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 transform hover:scale-105 active:scale-95"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Searching...
                </span>
              ) : (
                '🔍 Search Song'
              )}
            </button>
          </form>
        </div>

        {/* Info Section */}
        <div className="mt-8 text-center text-blue-200 text-sm">
          <p>Powered by Machine Learning • TF-IDF & Cosine Similarity</p>
        </div>
      </div>
    </div>
  );
};

export default HomePage;

