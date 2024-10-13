import './App.css';
import { TypeAnimation } from 'react-type-animation';
import { useState } from 'react';
import Webcam from "react-webcam";
import robot from "./robot.png"
import burger from "./burger.png"
import hotDog from "./hot-dog.png"
import pancakes from "./pancakes.png"
import donut from "./donut.png"

function App() {
  const [robotVisible, setRobot] = useState(true);
  const [buttonsVisible, setButtons] = useState(false);
  const [dialogueStep, setDialogueStep] = useState(0);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
  const [recipeInstructions, setRecipeInstructions] = useState([]);
  const [currentInstruction, setCurrentInstruction] = useState(0);
  const recipes = ["pancakes", "quesadillas", "omelette"];

  const handleRecipeClick = (recipe) => {
    setSelectedRecipe(recipe);
    setDialogueStep(1);
  };

  const dialogueSequences = [
    [
      () => {
        document.getElementById("robot").classList.add("App-robot")
      },
      '> Welcome to Virtual Chef.',
      () => {
        document.getElementById("robot").classList.remove("App-robot")
      },
      2000,
      () => {
        document.getElementById("robot").classList.add("App-robot")
      },
      '> Please choose a recipe.',
      () => {
        document.getElementById("robot").classList.remove("App-robot")
      },
      1000,
      () => setButtons(true)
    ],
    [
      () => {
        document.getElementById("robot").classList.add("App-robot")
      },
      `> You have chosen ${selectedRecipe}.`,
      () => {
        document.getElementById("robot").classList.remove("App-robot")
      },
      2000,
      () => {
        document.getElementById("robot").classList.add("App-robot")
      },
      '> Here is your recipe...',
      () => {
        document.getElementById("robot").classList.remove("App-robot")
      },
      async () => {
        // hide robot and food
        setRobot(false);
        
        // fetch recipe from flask server
        const response = await fetch(`http://127.0.0.1:5000/recipes/${selectedRecipe}`);
        const data = await response.json();
        const simpleInstructions = data.map(item => item.instruction);
        setRecipeInstructions(simpleInstructions);
      }
    ]
  ];

  return (
    <div className="App">
      <header className="App-header">
        {robotVisible && <div className="robot-container">
          <img id="robot" src={robot} width="50%" alt="Robot" />
          <img className="orbiting-image image1" src={burger} width="40%" alt="Burger" />
          <img className="orbiting-image image2" src={hotDog} width="40%" alt="Hot Dog" />
          <img className="orbiting-image image3" src={pancakes} width="40%" alt="Pancakes" />
          <img className="orbiting-image image4" src={donut} width="40%" alt="Donut" />
        </div>}
        <TypeAnimation
          key={dialogueStep}
          sequence={dialogueSequences[dialogueStep]}
          wrapper="span"
          speed={50}
          style={{ fontSize: '2em', display: 'inline-block', zIndex: 1, backgroundColor: "rgba(255, 255, 255, 0.5)", border: "3px solid black" }}
          repeat={0}
        />
        {dialogueStep === 0 && buttonsVisible && (
          <div>
            {recipes.map((recipe, index) => (
              <button style={{ fontFamily: "Pixel", color: "rgb(255, 0, 174)", fontSize: '1.25em', display: 'inline-block', zIndex: 2, backgroundColor: "rgba(255, 255, 255, 0.5)", border: "3px solid black", margin: 10, marginTop: 65 }} key={index} onClick={() => handleRecipeClick(recipe)}>
                {recipe}
              </button>
            ))}
          </div>
        )}
        {
          !robotVisible && (
            <div
              style={{
                padding: 20,
                marginTop: 20,
                backgroundColor: 'rgb(255, 0, 174)',
                border: "3px solid black",
                boxShadow: "10px 10px 5px rgba(0, 0, 0, 0.5)", // Add this line for a shadow effect
                fontFamily: 'Pixelify Sans',
                WebkitTextStrokeColor: 'gold',
                color: 'gold',
                width: "50%"
              }}
            >
              <Webcam style={{border: "3px solid black", width: "75%"}} />
              <div style={{backgroundColor: "purple", border: "3px solid black"}}>
                <p style={{fontSize: '30px', marginLeft: 10, marginRight: 10}}>{currentInstruction+1}. {recipeInstructions[currentInstruction]}</p>
                <div style={{border: "3px solid black", backgroundColor: 'white', marginBottom: 10, color: 'lime', WebkitTextStrokeColor: 'lime', fontSize: '30px', marginLeft: 10, marginRight: 10}}>(Click to verify completion.)</div>
              </div>
            </div>
          )
        }
      </header>
    </div>
  );
}

export default App;
