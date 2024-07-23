// // // src/App.js
// // import React, { useState } from 'react';
// // import './App.css';
// // import axios from 'axios';


// // function App() {
// //   const [prompt, setPrompt] = useState('');
// //   const [selectedFiles, setSelectedFiles] = useState(null);
// //   const [response, setResponse] = useState('');

// //   const handlePromptChange = (event) => {
// //     setPrompt(event.target.value);
// //   };

// //   const handleFileSelect = (event) => {
// //     setSelectedFiles(event.target.files);
// //   };

// //   const handleSubmit = async () => {
// //     if (!selectedFiles) {
// //       alert('Please select at least one file.');
// //       return;
// //     }
// //     const formData = new FormData();
// //     for (let i = 0; i < selectedFiles.length; i++) {
// //       formData.append('file', selectedFiles[i]);
// //     }
// //     formData.append('prompt', prompt);

// //     try {
// //       const res = await axios.post('http://localhost:8000/upload_and_analyze', formData, {
// //         headers: {
// //           'Content-Type': 'multipart/form-data',
// //         },
// //       });
// //       setResponse(res.data);
// //     } catch (error) {
// //       console.error('Error uploading files:', error);
// //       setResponse(error.message);
// //     }
// //   };
// // // ... rest of your component



// // // return (
// // //   <div className="App">
// // //     <header className="App-header">
// // //       {/* Add navigation bar items here */}
// // //       <div className="App-header-content">
// // //         <h1 className="App-title">Your One Stop Shop For Quality Properties</h1>
// // //         <p className="App-subtitle">Discover the future of home buying with Your One Stop Shop For Quality Properties. Our AI-driven inspections and ratings ensure you find top-quality homes effortlessly. Trust us to elevate your property search experience, making it seamless and reliable. Start your journey to the perfect home with us today.</p>
// // //         {/* ... rest of your input section */}
// // //       </div>
// // //       {/* ... rest of your header */}
// // //     </header>
// // //     <main className="App-main">
// // //       {/* ... rest of your main content */}
// // //     </main>
// // //   </div>
// // // );
// // // }

// // // export default App;


// // return (
// //   <div className="App">
// //     <div className="input-section">
// //       <input type="text" value={prompt} onChange={handlePromptChange} placeholder="Enter your prompt here" />
// //       <input type="file" multiple onChange={handleFileSelect} />
// //       <button onClick={handleSubmit}>Generate</button>
// //     </div>
// //     {response && (
// //       <div className="response-section">
// //         {/* Check if response properties are available before rendering */}
// //         {response.combined_score && <p>Score: {response.combined_score}</p>}
// //         {response.description && <p>Description: {response.description}</p>}
// //       </div>
// //     )}
// //   </div>
// // );
// //   }
// // export default App;



// // // src/App.js
// // import React, { useState } from 'react';
// // import './App.css';
// // import axios from 'axios';
// // import logo from './image1.png'; // Replace './logo.png' with the path to your logo image

// // function App() {
// //   const [prompt, setPrompt] = useState('');
// //   const [selectedFiles, setSelectedFiles] = useState([]);
// //   const [response, setResponse] = useState(null);

// //   const handlePromptChange = (event) => {
// //     setPrompt(event.target.value);
// //   };

// //   const handleFileSelect = (event) => {
// //     setSelectedFiles(event.target.files);
// //   };

// //   const handleSubmit = async () => {
// //     if (selectedFiles.length === 0) {
// //       alert('Please select at least one file.');
// //       return;
// //     }

// //     const formData = new FormData();
// //     for (let file of selectedFiles) {
// //       formData.append('file', file);
// //     }
// //     formData.append('prompt', prompt);

// //     try {
// //       const res = await axios.post('http://localhost:8000/upload_and_analyze', formData, {
// //         headers: {
// //           'Content-Type': 'multipart/form-data',
// //         },
// //       });
// //       setResponse(res.data);
// //     } catch (error) {
// //       console.error('Error uploading files:', error);
// //       setResponse({ error: error.message });
// //     }
// //   };

// import React, { useState } from 'react';
// import './App.css'; // Make sure your CSS is correctly linked
// import axios from 'axios';
// import people from './assets/people.png'; // Ensure the path to your image is correct
// import ai from './assets/ai.png'; // Ensure the path to your image is correct

// function App() {
//   const [prompt, setPrompt] = useState('');
//   const [selectedFiles, setSelectedFiles] = useState([]);
//   const [response, setResponse] = useState(null);

//   const handlePromptChange = (event) => {
//     setPrompt(event.target.value);
//   };

//   const handleFileSelect = (event) => {
//     setSelectedFiles(event.target.files);
//   };

//   const handleSubmit = async () => {
//         if (selectedFiles.length === 0) {
//           alert('Please select at least one file.');
//           return;
//         }
    
//         const formData = new FormData();
//         for (let file of selectedFiles) {
//           formData.append('file', file);
//         }
//         formData.append('prompt', prompt);
    
//         try {
//           const res = await axios.post('http://localhost:8000/upload_and_analyze', formData, {
//             headers: {
//               'Content-Type': 'multipart/form-data',
//             },
//           });
//           setResponse(res.data);
//         } catch (error) {
//           console.error('Error uploading files:', error);
//           setResponse({ error: error.message });
//         }
//       };

//   return (
//     <div className="App">
//       <div className="gpt3__header section__padding" id="home">
//         <div className="gpt3__header-content">
//           <h1 className="gradient__text">Your One Stop Shop For Quality Properties</h1>
//           <p>Discover the future of home buying with Your One Stop Shop For Quality Properties. Our AI-driven inspections and ratings ensure you find top-quality homes effortlessly. Trust us to elevate your property search experience, making it seamless and reliable. Start your journey to the perfect home with us today.</p>

//           <div className="gpt3__header-content__input">
//             <input type="text" placeholder="Enter your prompt here" value={prompt} onChange={handlePromptChange} />
//             <input type="file" multiple onChange={handleFileSelect} />
//             <button type="button" onClick={handleSubmit}>Generate</button>
//           </div>

//           <div className="gpt3__header-content__people">
//             <img src={people} alt="People" />
//             <p>1,600 people requested access a visit in last 24 hours</p>
//           </div>
//         </div>

//         <div className="gpt3__header-image">
//           <img src={ai} alt="AI" />
//         </div>
//       </div>

//       {response && (
//         <div className="response-section">
//           {/* Display the response here */}
//         </div>
//       )}
//     </div>
//   );
// }

// export default App;


// //   return (
// //     <div className="App">
// //       <header className="App-header">
// //         <nav className="App-nav">
// //         <img src={logo} />
// //           {/* Replace # with actual paths */}
// //           <a href="#">Home</a>
// //           <a href="#">What is GPT3?</a>
// //           {/* ... other nav items */}
// //           <a href="#" className="App-nav-signin">Sign In</a>
// //           <a href="#" className="App-nav-signup">Sign Up</a>
// //         </nav>
// //         <div className="App-header-content">
// //           <h1 className="App-title">Your One Stop Shop For Quality Properties</h1>
// //           <p className="App-subtitle">Discover the future of home buying with Your One Stop Shop For Quality Properties. Our AI-driven inspections and ratings ensure you find top-quality homes effortlessly. Trust us to elevate your property search experience, making it seamless and reliable. Start your journey to the perfect home with us today.</p>
// //           <input type="text" value={prompt} onChange={handlePromptChange} placeholder="Enter your prompt here" />
// //           <input type="file" multiple onChange={handleFileSelect} />
// //           <button onClick={handleSubmit}>Generate</button>
// //         </div>
// //       </header>
// //       <main className="App-main">
// //         {response && (
// //           <div className="response-section">
// //             {response.error ? (
// //               <p className="error-message">{response.error}</p>
// //             ) : (
// //               <>
// //                 {response.combined_score && <p className="score">Score: {response.combined_score}</p>}
// //                 {response.description && <p className="description">{response.description}</p>}
// //               </>
// //             )}
// //           </div>
// //         )}
// //       </main>
// //     </div>
// //   );
// // }

// // export default App;

// //   return (
// //     <div className="App gradient__bg">
// //       <header className="App-header section__padding">
// //         <nav className="App-nav">
// //           <img src={logo} alt="Logo" className="App-logo" />
// //           <a href="#" className="App-nav-link">Home</a>
// //           <a href="#" className="App-nav-link">What is GPT3?</a>
// //           {/* ... other nav items */}
// //           <a href="#" className="App-nav-signin">Sign In</a>
// //           <a href="#" className="App-nav-signup">Sign Up</a>
// //         </nav>
// //         <div>
// //   <div className="gpt3__header section__padding" id="home">
// //     <div className="gpt3__header-content">
// //       <h1 className="gradient__text">Your One Stop Shop For Quality Properties</h1>
// //       <p>Discover the future of home buying with Your One Stop Shop For Quality Properties. Our AI-driven inspections and ratings ensure you find top-quality homes effortlessly. Trust us to elevate your property search experience, making it seamless and reliable. Start your journey to the perfect home with us today.</p>

// //       <div className="gpt3__header-content__input">
// //         <input type="text" placeholder="Enter your prompt here" value={prompt} onChange={onPromptChange} />
// //         <input type="file" multiple onChange={onFileSelect} />
// //         <button type="button" onClick={onSubmit}>Generate</button>
// //       </div>

// //       <div className="gpt3__header-content__people">
// //         <img src={people} alt="People" />
// //         <p>1,600 people requested access a visit in last 24 hours</p>
// //       </div>
// //     </div>

// //     <div className="gpt3__header-image">
// //       <img src={ai} alt="AI" />
// //     </div>
// //   </div>
// //   </div>

// // export default Header;
// //         <div className="App-header-content">
// //           <h1 className="App-title gradient__text">Your One Stop Shop For Quality Properties</h1>
// //           <p className="App-subtitle">Discover the future of home buying with Your One Stop Shop For Quality Properties. Our AI-driven inspections and ratings ensure you find top-quality homes effortlessly. Trust us to elevate your property search experience, making it seamless and reliable. Start your journey to the perfect home with us today.</p>
// //           <div className="input-section">
// //             <input type="text" value={prompt} onChange={handlePromptChange} placeholder="Enter your prompt here" className="prompt-input" />
// //             <input type="file" multiple onChange={handleFileSelect} className="file-input" />
// //             <button onClick={handleSubmit} className="generate-button">Generate</button>
// //           </div>
// //         </div>
// //       </header>
// //       <main className="App-main section__padding">
// //         {response && (
// //           <div className="response-section scale-up-center">
// //             {response.error ? (
// //               <p className="error-message">{response.error}</p>
// //             ) : (
// //               <>
// //                 {response.combined_score && <p className="score">Score: {response.combined_score}</p>}
// //                 {response.description && <p className="description">{response.description}</p>}
// //               </>
// //             )}
// //           </div>
// //         )}
// //       </main>
// //     </div>
// //   );
// // }

// // export default App;

import React, { useState } from 'react';
import './App.css';
import axios from 'axios';
import logo from './image1.png'; // Make sure to replace './logo.png' with the path to your logo image

function App() {
  const [prompt, setPrompt] = useState('');
  const [address, setAddress] = useState('');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [response, setResponse] = useState(null);

  const handlePromptChange = (event) => {
    setPrompt(event.target.value);
  };

  const handleFileSelect = (event) => {
    setSelectedFiles(event.target.files);
  };

  const handleAddressChange = (event) => {
    setAddress(event.target.value);
  };

  const handleSubmit = async () => {
        if (selectedFiles.length === 0) {
          alert('Please select at least one file.');
          return;
        }
    
        const formData = new FormData();
        for (let file of selectedFiles) {
          formData.append('file', file);
        }
        formData.append('prompt', prompt);
        formData.append('address', address);
    
        try {
          const res = await axios.post('http://localhost:8000/upload_and_analyze', formData, {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          });
          setResponse(res.data);
        } catch (error) {
          console.error('Error uploading files:', error);
          setResponse({ error: error.message });
        }
      };

  return (
    <div className="App">
      <div className="App-header">
        <img src={logo} alt="Logo" className="App-logo" />
        <input 
          type="text" 
          value={prompt} 
          onChange={handlePromptChange} 
          placeholder="Enter your prompt" 
          className="prompt-input"
        />
        <input 
          type="file" 
          multiple
          onChange={handleFileSelect} 
          className="file-input"
        />
        <input 
          type="text" 
          value={address}
          onChange={handleAddressChange}
          placeholder="Enter your address"
          className="prompt-address"
        />

        <button onClick={handleSubmit} className="submit-button">Upload</button>
      </div>
      {response && (
        <div className="response-section">
        <div className="score-scale">
          <div className="score-pointer" style={{ left: `${response.combined_score}%` }}></div>
        </div>
        <p>Score: {response.combined_score}</p>
        
        {/* Assuming ';' is used as a delimiter in the description string */}
        <ul>
          {response.description.split('. ').map((point, index) => (
            <li key={index}>{point}</li>
          ))}
        </ul>
      </div>
      )}
    </div>
  );
}

export default App;
