
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCrosshairs } from "@fortawesome/free-solid-svg-icons";
function DataCard({item, objects}) {
  return (
    <div className='data-card'>
        <div className="left">
          <h3>{item}</h3>
      <p>{objects} detected objects</p>  
        </div>
        <button className='target'>
          <FontAwesomeIcon icon={faCrosshairs} />
        </button>
      
    </div>
  )
}

export default DataCard
