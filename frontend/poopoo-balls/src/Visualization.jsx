import DataSet from './components/DataSet'
import IconTag from './components/IconTag'
import { faCloud, faCloudRain, faSnowflake} from "@fortawesome/free-solid-svg-icons";
import ReactSlider from "react-slider";
import VisualizationChart from './components/VisualizationChart';

function Visualization() {
  return (
    <div className='page visual'>
        {/* need to map this */}
        <div className="left-panel">
          <div className="original-image-contain">
            <div className="tag">Original image</div>
            <img src="exampleImage.png" alt="" />
          </div>
           <DataSet
        item="Helmet"
        objects="33"
        infoSize = "200"
        objectCount = "3"
      >
        
      </DataSet>
      <VisualizationChart></VisualizationChart>
        </div>
        <div className="right-panel">
          <div className="tag-row">
            <IconTag
              tagName="Original"
              iconName=""
            ></IconTag>
            <IconTag
              tagName="Cloud"
              iconName={faCloudRain}
            ></IconTag>
            <IconTag
              tagName="Fog"
              iconName={faCloud}
            ></IconTag>
            <IconTag
              tagName="Snow"
              iconName={faSnowflake}
            ></IconTag>

           
          </div>
          <div className="main-image">
            <img src="exampleImage.png" />
          </div>
          <div className="slider-contain">
            <div className="slider-row-contain">

                <p>Original image</p>
                <p>Augmented image</p>
                
            </div>
            <ReactSlider
              className="horizontal-slider"
              thumbClassName="example-thumb"
              trackClassName="example-track"
            />
          </div>
          
        </div>
     
    </div>
  )
}

export default Visualization