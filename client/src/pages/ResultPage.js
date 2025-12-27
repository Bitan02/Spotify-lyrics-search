import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const ResultPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  
  // Get data from navigation state
  const { song, artist, confidence, lyrics } = location.state || {};

  // Redirect to home if no data (must be called unconditionally)
  React.useEffect(() => {
    if (!song || !artist) {
      navigate('/');
    }
  }, [song, artist, navigate]);

  // If no data, show nothing while redirecting
  if (!song || !artist) {
    return null;
  }

  // Calculate confidence percentage and color
  const confidencePercent = (confidence * 100).toFixed(1);
  const confidenceColor = confidence > 0.7 
    ? 'text-green-400' 
    : confidence > 0.4 
    ? 'text-yellow-400' 
    : 'text-red-400';

  const handleNewSearch = () => {
    navigate('/');
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-12">
      <div className="max-w-2xl w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            🎵 Search Result
          </h1>
        </div>

        {/* Result Card */}
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl shadow-2xl p-8 border border-white/20">
          {/* Song Info */}
          <div className="text-center mb-8">
            <div className="mb-4">
              <h2 className="text-3xl font-bold text-white mb-2">{song}</h2>
              <p className="text-xl text-blue-200">by {artist}</p>
            </div>

            {/* Confidence Score */}
            <div className="inline-block bg-white/10 rounded-lg px-6 py-3 mb-6">
              <p className="text-sm text-blue-200 mb-1">Confidence Score</p>
              <p className={`text-3xl font-bold ${confidenceColor}`}>
                {confidencePercent}%
              </p>
            </div>
          </div>

          {/* Original Lyrics */}
          <div className="mb-6">
            <h3 className="text-lg font-semibold text-white mb-3">
              Your Search:
            </h3>
            <div className="bg-white/5 rounded-lg p-4 border border-white/10">
              <p className="text-blue-100 whitespace-pre-wrap italic">
                "{lyrics}"
              </p>
            </div>
          </div>

          {/* Confidence Explanation */}
          <div className="bg-blue-500/20 border border-blue-400/50 rounded-lg p-4 mb-6">
            <p className="text-sm text-blue-200">
              <strong>Confidence Score:</strong> This indicates how closely the 
              lyrics match the identified song. Higher scores (70%+) indicate 
              stronger matches. Lower scores may indicate the song isn't in our 
              database or the lyrics snippet is too short.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex gap-4">
            <button
              onClick={handleNewSearch}
              className="flex-1 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 transform hover:scale-105 active:scale-95"
            >
              🔍 New Search
            </button>
          </div>
        </div>

        {/* Back to Home */}
        <div className="mt-6 text-center">
          <button
            onClick={() => navigate('/')}
            className="text-blue-200 hover:text-white transition-colors"
          >
            ← Back to Home
          </button>
        </div>
      </div>
    </div>
  );
};

export default ResultPage;

