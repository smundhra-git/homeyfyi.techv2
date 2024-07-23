// src/components/header/Header.jsx
import React from 'react';
import people from '../../assets/people.png';
import ai from '../../assets/ai.png';
import './header.css';

const Header = ({ prompt, onPromptChange, onFileSelect, onSubmit }) => (
  <div className="gpt3__header section__padding" id="home">
    <div className="gpt3__header-content">
      <h1 className="gradient__text">Your One Stop Shop For Quality Properties</h1>
      <p>Discover the future of home buying with Your One Stop Shop For Quality Properties. Our AI-driven inspections and ratings ensure you find top-quality homes effortlessly. Trust us to elevate your property search experience, making it seamless and reliable. Start your journey to the perfect home with us today.</p>

      <div className="gpt3__header-content__input">
        <input type="text" placeholder="Enter your prompt here" value={prompt} onChange={onPromptChange} />
        <input type="file" multiple onChange={onFileSelect} />
        <button type="button" onClick={onSubmit}>Generate</button>
      </div>

      <div className="gpt3__header-content__people">
        <img src={people} alt="People" />
        <p>1,600 people requested access a visit in last 24 hours</p>
      </div>
    </div>

    <div className="gpt3__header-image">
      <img src={ai} alt="AI" />
    </div>
  </div>
);

export default Header;
