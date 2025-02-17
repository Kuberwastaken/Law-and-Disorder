import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import Header from './Header';
import './LandingPage.css';

const teamMembers = [
  {
    name: "Kuber Mehta",
    role: "Lead Developer, Backend, AI Training",
    image: "https://avatars.githubusercontent.com/u/97027230",
    github: "https://github.com/Kuberwastaken",
  },
  {
    name: "Parrv Luthra",
    role: "Frontend Design",
    image: "https://avatars.githubusercontent.com/u/183385896?v=4",
    github: "https://github.com/parrvluthra22",
  },
  {
    name: "Anant Singhal",
    role: "App Development",
    image: "https://avatars.githubusercontent.com/u/89266869?v=4",
    github: "https://github.com/GithubAnant",
  },
  {
    name: "Gargi Srivastava",
    role: "Frontend Design",
    image: "https://avatars.githubusercontent.com/u/184646682?v=4",
    github: "https://github.com/gigibyte2024",
  },
];

function LandingPage() {
  const navigate = useNavigate();

  useEffect(() => {
    const updateMousePosition = (e) => {
      const hero = document.querySelector('.hero-section');
      if (!hero) return;
      
      const { clientX, clientY } = e;
      const { left, top, width, height } = hero.getBoundingClientRect();
      const x = (clientX - left) / width;
      const y = (clientY - top) / height;
      
      hero.style.setProperty('--mouse-x', x);
      hero.style.setProperty('--mouse-y', y);
    };

    window.addEventListener('mousemove', updateMousePosition);
    return () => window.removeEventListener('mousemove', updateMousePosition);
  }, []);

  return (
    <div className="landing-page">
      <Header /> {/* ✅ Include the header component */}

      <div className="grid-overlay"></div>

      <section className="hero-section" id="home">
        <div className="hero-gradient"></div>
        <motion.div 
          className="hero-content"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <motion.h1 
            className="hero-title"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
          >
            Law &amp; Disorder
          </motion.h1>
          <motion.p 
            className="hero-subtitle"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            A Party Game for the Legally Curious
          </motion.p>
          <motion.p 
            className="hero-description"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.6 }}
          >
            Explore the boundaries of Indian law through AI-powered analysis. 
            Submit your wildest scenarios and watch as our legal engine determines 
            their constitutional validity. Learning law has never been this entertaining.
          </motion.p>
          <motion.div 
            className="hero-buttons"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.8 }}
          >
            <button 
              className="btn primary-btn"
              onClick={() => navigate('/game')}
            >
              Try It Out
            </button>
            <a
              href="https://github.com/Kuberwastaken/Law-and-Disorder"
              target="_blank"
              rel="noopener noreferrer"
              className="btn secondary-btn"
            >
              View Source
            </a>
          </motion.div>
        </motion.div>
      </section>

      <motion.section 
        className="mission-section"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <h2>Our Mission</h2>
        <div className="mission-content">
          <p>
            Legal education shouldn't be confined to dusty textbooks and monotonous lectures. 
            We're revolutionizing how people learn about law through interactive gaming experiences 
            that make complex legal concepts accessible and entertaining.
          </p>
          <p>
            By combining cutting-edge AI technology with gamification, we're creating a new 
            paradigm for legal education that engages, entertains, and educates simultaneously.
          </p>
        </div>
      </motion.section>

      <motion.section 
        className="features-section"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <div className="features-grid">
          <motion.div 
            className="feature-card"
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <h3>AI-Powered Analysis</h3>
            <p>Real-time constitutional analysis using cutting-edge AI models</p>
          </motion.div>
          <motion.div 
            className="feature-card"
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <h3>Interactive Learning</h3>
            <p>Learn complex legal concepts through engaging gameplay</p>
          </motion.div>
          <motion.div 
            className="feature-card"
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 300 }}
          >
            <h3>Social Experience</h3>
            <p>Perfect for parties, classrooms, and legal enthusiasts</p>
          </motion.div>
        </div>
      </motion.section>

      <motion.section 
        className="about-section"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <h2>Why "Future Layoffs"?</h2>
        <div className="about-content">
          <p>
            Our name "Future Layoffs" is both a statement and a vision. We believe AI should 
            handle mundane, repetitive tasks, effectively "laying off" humans from boring work. 
            This technological shift isn't about replacement—it's about liberation.
          </p>
          <p>
            We envision a future where AI empowers humans to pursue more meaningful, creative, 
            and fulfilling endeavors. By automating the routine, we free ourselves to focus on 
            what makes us uniquely human: creativity, emotional intelligence, and complex problem-solving.
          </p>
        </div>
      </motion.section>

      <motion.section 
        className="team-section"
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
        viewport={{ once: true }}
      >
        <h2>Meet The Team</h2>
        <div className="team-grid">
          {teamMembers.map((member, idx) => (
            <motion.div 
              className="team-card"
              key={idx}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              viewport={{ once: true }}
              whileHover={{ y: -10 }}
            >
              <div className="team-card-image">
                <img src={member.image} alt={member.name} />
              </div>
              <div className="team-card-info">
                <h3>
                  <a href={member.github} target="_blank" rel="noopener noreferrer">
                    {member.name}
                  </a>
                </h3>
                <p>{member.role}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.section>

      <footer className="footer-section">
        <p>
          Created for the <strong>Code Genesis Hackathon</strong>
          <br />© {new Date().getFullYear()} Team Future Layoffs
        </p>
      </footer>
    </div>
  );
}

export default LandingPage;
