import './App.css';
import { TypeAnimation } from 'react-type-animation';
import { useSpring, animated } from '@react-spring/web'
import robot from "./robot.png"

function App() {
  const [springs, api] = useSpring(() => ({
    from: { translateY: 0 },
    to: { translateY: -10 },
  }));

  const triggerAnimation = () => {
    api.start({
      from: { translateY: 0 },
      to: { translateY: -10 },
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <img id="robot" src={robot} width="15%" alt="Robot" />
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
          style={{ fontSize: '2em', display: 'inline-block' }}
          repeat={0}
        />
      </header>
    </div>
  );
}

export default App;
