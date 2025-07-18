import { useState, useEffect } from 'react';
import { FaComments } from 'react-icons/fa';
import { MdDarkMode } from 'react-icons/md';
import { Link } from 'react-router-dom';

const Header = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Toggle dark mode class on <html>
  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <header className="bg-white dark:bg-gray-900 shadow-md sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between items-center h-16">
        {/* Logo */}
        <Link to="/" className="flex items-center space-x-2">
          <FaComments className="text-indigo-600 dark:text-indigo-400 text-2xl" />
          <span className="text-xl font-bold text-gray-800 dark:text-white">ZenithAi</span>
        </Link>

        {/* Desktop menu */}
        <nav className="hidden md:flex items-center space-x-6">
          <Link to="/features" className="text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400">
            Features
          </Link>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400"
            title="Toggle Dark Mode"
          >
            <MdDarkMode size={22} />
          </button>
          <Link
            to="/login"
            className="px-4 py-1 border border-indigo-600 text-indigo-600 rounded hover:bg-indigo-100 dark:border-indigo-400 dark:text-indigo-400 dark:hover:bg-gray-800 transition"
          >
            Login
          </Link>
          <Link
            to="/signup"
            className="px-4 py-1 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition"
          >
            Sign Up
          </Link>
        </nav>

        {/* Mobile menu button */}
        <button
          className="md:hidden text-gray-700 dark:text-gray-300 focus:outline-none"
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
        >
          <svg className="h-6 w-6" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            {mobileMenuOpen ? (
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            ) : (
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h16M4 12h16M4 18h16" />
            )}
          </svg>
        </button>
      </div>

      {/* Mobile dropdown menu */}
      {mobileMenuOpen && (
        <div className="md:hidden px-4 pb-4 space-y-2">
          <Link to="/features" className="block text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400">
            Features
          </Link>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="block text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400"
          >
            Toggle Dark Mode
          </button>
          <Link
            to="/login"
            className="block text-indigo-600 dark:text-indigo-400 border border-indigo-600 dark:border-indigo-400 px-4 py-1 rounded hover:bg-indigo-100 dark:hover:bg-gray-800"
          >
            Login
          </Link>
          <Link
            to="/signup"
            className="block bg-indigo-600 text-white px-4 py-1 rounded hover:bg-indigo-700"
          >
            Sign Up
          </Link>
        </div>
      )}
    </header>
  );
};

export default Header;
