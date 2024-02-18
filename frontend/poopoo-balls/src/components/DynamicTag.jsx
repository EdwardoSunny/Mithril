function DynamicTag({ tagName, condition }) {
  return <div className={`tag clickable ${condition}`}>{tagName}</div>;
}

export default DynamicTag;
