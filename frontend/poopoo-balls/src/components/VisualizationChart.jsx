
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBullseye } from "@fortawesome/free-solid-svg-icons";
function VisualizationChart() {
  return (
    <div className="visualization-contain">
      <h3>Visualization</h3>
      <div className="target-contain">
        <h4>Target:</h4>
        <div className="tag" style={{backgroundColor:'#151716', border: '2px solid rgba(255, 255, 255, .1)'}}>
            <FontAwesomeIcon icon={faBullseye} style={{color:'#00BFA8'}}/>
            98% accuracy
        </div>
        <img src="visualizationPNG.svg" alt="" />
      </div>
      
    </div>
  )
}

export default VisualizationChart
