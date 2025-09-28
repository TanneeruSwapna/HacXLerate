import { Link } from 'react-router-dom';
import './AboutPage.css';

function AboutPage() {
    return (
        <div className="about-page">
            {/* Hero Section */}
            <section className="about-hero">
                <div className="container">
                    <div className="hero-content">
                        <div className="hero-badge">
                            <span className="badge-icon">🏢</span>
                            <span>About Qwipo</span>
                        </div>
                        <h1 className="hero-title">
                            Empowering B2B Commerce Through Technology
                        </h1>
                        <p className="hero-subtitle">
                            We're building the future of business-to-business commerce, connecting companies
                            worldwide through innovative technology and intelligent solutions.
                        </p>
                    </div>
                </div>
            </section>

            {/* Mission Section */}
            <section className="mission-section">
                <div className="container">
                    <div className="mission-content">
                        <div className="mission-text">
                            <h2 className="section-title">Our Mission</h2>
                            <p className="section-description">
                                To revolutionize B2B commerce by creating a seamless, intelligent platform that
                                connects businesses, streamlines operations, and drives growth through data-driven
                                insights and AI-powered recommendations.
                            </p>
                            <p className="section-description">
                                We believe that every business deserves access to cutting-edge tools that can
                                transform their operations and unlock new opportunities in the global marketplace.
                            </p>
                        </div>
                        <div className="mission-visual">
                            <div className="mission-card">
                                <div className="card-icon">🎯</div>
                                <h3>Innovation</h3>
                                <p>Pioneering the next generation of B2B commerce solutions</p>
                            </div>
                            <div className="mission-card">
                                <div className="card-icon">🤝</div>
                                <h3>Connection</h3>
                                <p>Building bridges between businesses worldwide</p>
                            </div>
                            <div className="mission-card">
                                <div className="card-icon">📈</div>
                                <h3>Growth</h3>
                                <p>Empowering businesses to scale and succeed</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Story Section */}
            <section className="story-section">
                <div className="container">
                    <div className="story-content">
                        <div className="story-text">
                            <h2 className="section-title">Our Story</h2>
                            <p className="section-description">
                                Founded in 2024, Qwipo emerged from a simple yet powerful vision: to transform
                                how businesses connect and trade with each other. Our founders, experienced
                                entrepreneurs in the B2B space, recognized the need for a more intelligent,
                                user-friendly platform that could adapt to the evolving needs of modern commerce.
                            </p>
                            <p className="section-description">
                                Starting as a small team with big dreams, we've grown into a comprehensive
                                B2B marketplace that serves thousands of businesses across multiple industries.
                                Our journey has been marked by continuous innovation, user feedback integration,
                                and a commitment to excellence.
                            </p>
                        </div>
                        <div className="story-timeline">
                            <div className="timeline-item">
                                <div className="timeline-year">2024</div>
                                <div className="timeline-content">
                                    <h4>Platform Launch</h4>
                                    <p>Qwipo B2B Marketplace officially launches with core features</p>
                                </div>
                            </div>
                            <div className="timeline-item">
                                <div className="timeline-year">Q2 2024</div>
                                <div className="timeline-content">
                                    <h4>AI Integration</h4>
                                    <p>Advanced machine learning recommendations system goes live</p>
                                </div>
                            </div>
                            <div className="timeline-item">
                                <div className="timeline-year">Q3 2024</div>
                                <div className="timeline-content">
                                    <h4>Global Expansion</h4>
                                    <p>Platform expands to serve businesses in 50+ countries</p>
                                </div>
                            </div>
                            <div className="timeline-item">
                                <div className="timeline-year">Q4 2024</div>
                                <div className="timeline-content">
                                    <h4>Enterprise Features</h4>
                                    <p>Advanced analytics and enterprise-grade security features released</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* Values Section */}
            <section className="values-section">
                <div className="container">
                    <div className="section-header">
                        <h2 className="section-title">Our Values</h2>
                        <p className="section-subtitle">
                            The principles that guide everything we do
                        </p>
                    </div>
                    <div className="values-grid">
                        <div className="value-card">
                            <div className="value-icon">🔒</div>
                            <h3 className="value-title">Security First</h3>
                            <p className="value-description">
                                Enterprise-grade security and data protection are at the core of our platform,
                                ensuring your business information is always safe.
                            </p>
                        </div>
                        <div className="value-card">
                            <div className="value-icon">🚀</div>
                            <h3 className="value-title">Innovation</h3>
                            <p className="value-description">
                                We continuously push the boundaries of what's possible in B2B commerce,
                                leveraging cutting-edge technology to solve real business problems.
                            </p>
                        </div>
                        <div className="value-card">
                            <div className="value-icon">👥</div>
                            <h3 className="value-title">User-Centric</h3>
                            <p className="value-description">
                                Every feature we build starts with understanding our users' needs and
                                creating solutions that truly make their lives easier.
                            </p>
                        </div>
                        <div className="value-card">
                            <div className="value-icon">🌍</div>
                            <h3 className="value-title">Global Impact</h3>
                            <p className="value-description">
                                We believe in the power of technology to connect businesses worldwide
                                and create opportunities for growth across all markets.
                            </p>
                        </div>
                        <div className="value-card">
                            <div className="value-icon">📊</div>
                            <h3 className="value-title">Data-Driven</h3>
                            <p className="value-description">
                                Our decisions are backed by data and analytics, ensuring we build
                                features that deliver real value to our users.
                            </p>
                        </div>
                        <div className="value-card">
                            <div className="value-icon">🤝</div>
                            <h3 className="value-title">Partnership</h3>
                            <p className="value-description">
                                We work closely with our users and partners to co-create solutions
                                that address the unique challenges of modern B2B commerce.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Team Section */}
            <section className="team-section">
                <div className="container">
                    <div className="section-header">
                        <h2 className="section-title">Meet Our Team</h2>
                        <p className="section-subtitle">
                            The passionate people behind Qwipo's success
                        </p>
                    </div>
                    <div className="team-grid">
                        <div className="team-card">
                            <div className="team-avatar">
                                <span className="avatar-icon">👨‍💼</span>
                            </div>
                            <h3 className="team-name">Alex Johnson</h3>
                            <p className="team-role">CEO & Founder</p>
                            <p className="team-bio">
                                Former VP of Business Development at a Fortune 500 company,
                                Alex brings 15+ years of B2B experience to Qwipo.
                            </p>
                        </div>
                        <div className="team-card">
                            <div className="team-avatar">
                                <span className="avatar-icon">👩‍💻</span>
                            </div>
                            <h3 className="team-name">Sarah Chen</h3>
                            <p className="team-role">CTO & Co-Founder</p>
                            <p className="team-bio">
                                AI and machine learning expert with a PhD in Computer Science.
                                Sarah leads our technical innovation and product development.
                            </p>
                        </div>
                        <div className="team-card">
                            <div className="team-avatar">
                                <span className="avatar-icon">👨‍🎨</span>
                            </div>
                            <h3 className="team-name">Michael Rodriguez</h3>
                            <p className="team-role">Head of Design</p>
                            <p className="team-bio">
                                Award-winning UX designer with a focus on creating intuitive
                                business applications that users love to use.
                            </p>
                        </div>
                    </div>
                </div>
            </section>

            {/* Stats Section */}
            <section className="stats-section">
                <div className="container">
                    <div className="stats-grid">
                        <div className="stat-item">
                            <div className="stat-number">10,000+</div>
                            <div className="stat-label">Active Businesses</div>
                        </div>
                        <div className="stat-item">
                            <div className="stat-number">$50M+</div>
                            <div className="stat-label">Total Transaction Volume</div>
                        </div>
                        <div className="stat-item">
                            <div className="stat-number">150+</div>
                            <div className="stat-label">Countries Served</div>
                        </div>
                        <div className="stat-item">
                            <div className="stat-number">99.9%</div>
                            <div className="stat-label">Uptime</div>
                        </div>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="about-cta">
                <div className="container">
                    <div className="cta-content">
                        <h2 className="cta-title">Ready to Join Our Community?</h2>
                        <p className="cta-subtitle">
                            Be part of the future of B2B commerce
                        </p>
                        <div className="cta-actions">
                            <Link to="/register" className="btn btn-primary btn-large">
                                Get Started Today
                            </Link>
                            <Link to="/login" className="btn btn-outline btn-large">
                                Sign In
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

        </div>
    );
}

export default AboutPage;
