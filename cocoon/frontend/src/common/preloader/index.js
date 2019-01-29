import React, {Component} from 'react';
import PropTypes from 'prop-types';
import './preloader.css';

export default class Preloader extends Component  {

  static defaultProps = {
    color: 'var(--red)',
    size: 10
  }

  static propTypes = {
    color: PropTypes.string.isRequired,
    size: PropTypes.number.isRequired
  }

  render() {
    const style = {
      background: this.props.color,
      height: this.props.size,
      width: this.props.size,
      margin: this.props.size / 2
    }
    return (
      <div className="preloader">
        <span style={style} className="preloader-dot"></span>
        <span style={style} className="preloader-dot"></span>
        <span style={style} className="preloader-dot"></span>
      </div>
    );
  }
}