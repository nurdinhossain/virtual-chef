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
        <img class="App-robot" src={robot} width="15%" alt="Robot" />
        <TypeAnimation
          sequence={[
            '> Welcome to Virtual Chef.',
            2000,
            '> Please choose a recipe.',
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
