import './App.css';
import { TypeAnimation } from 'react-type-animation';
import robot from "./robot.png"
import burger from "./burger.png"
import hotDog from "./hot-dog.png"
import pancakes from "./pancakes.png"
import donut from "./donut.png"

function App() {
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
          sequence={[
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
            2000
          ]}
          wrapper="span"
          speed={50}
          style={{ fontSize: '2em', display: 'inline-block', zIndex: 1, backgroundColor: "rgba(255, 255, 255, 0.5)", border: "3px solid black" }}
          repeat={0}
        />
      </header>
    </div>
  );
}

export default App;
