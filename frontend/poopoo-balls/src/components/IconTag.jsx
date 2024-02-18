import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

function IconTag({ tagName, iconName }) {
    return <div className="tag clickable">
        <FontAwesomeIcon icon={iconName} />
        {tagName}
        </div>;
  }

export default IconTag
