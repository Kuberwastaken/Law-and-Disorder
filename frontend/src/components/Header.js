import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

function Header() {
  return (
    <header className="site-header">
      <div className="header-content">
        <div className="logo">
          <Link to="/">Future Layoffs</Link>
        </div>
        <nav className="nav-menu">
          <a href="#home">Home</a>
          <a href="#mission">Our Mission</a>
          <a href="#about">Why Future Layoffs?</a>
          <a href="#team">Team</a>
        </nav>
        <div className="spacer"></div>
      </div>
    </header>
  );
}

export default Header;
