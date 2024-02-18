function DynamicTag({ tagName, condition }) {
  return <div className={`tag ${condition}`}>{tagName}</div>;
}

export default DynamicTag;
