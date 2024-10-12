import './App.css';
import { TypeAnimation } from 'react-type-animation';
import { useState } from 'react';
import robot from "./robot.png"
import burger from "./burger.png"
import hotDog from "./hot-dog.png"
import pancakes from "./pancakes.png"
import donut from "./donut.png"

function App() {
  const [buttonsVisible, setButtons] = useState(false);
  const [dialogueStep, setDialogueStep] = useState(0);
  const [selectedRecipe, setSelectedRecipe] = useState(null);
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
      2000
    ]
  ];

  return (
    <div className="App">
      <header className="App-header">
        <div className="robot-container">
          <img id="robot" src={robot} width="50%" alt="Robot" />
          <img className="orbiting-image image1" src={burger} width="40%" alt="Burger" />
          <img className="orbiting-image image2" src={hotDog} width="40%" alt="Hot Dog" />
          <img className="orbiting-image image3" src={pancakes} width="40%" alt="Pancakes" />
          <img className="orbiting-image image4" src={donut} width="40%" alt="Donut" />
        </div>
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
      </header>
    </div>
  );
}

export default App;
