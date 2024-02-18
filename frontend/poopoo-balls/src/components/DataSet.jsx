import DataCard from "./DataCard"
function DataSet({infoSize, objectCount, item, objects}) {
  return (
    
      <div className="dataset-contain">
        <h3>Total dataset</h3>
        <p>{infoSize} of information</p>
        <div className="tag">{objectCount} objects detected</div>
        <DataCard
            item={item}
            objects={objects}
        >

        </DataCard>
        <DataCard
            item={item}
            objects={objects}
        >

        </DataCard>
        <DataCard
            item={item}
            objects={objects}
        >

        </DataCard>
      </div>
   
  )
}

export default DataSet
