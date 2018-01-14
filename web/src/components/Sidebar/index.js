// @flow
import React from 'react';
import { Link } from 'react-router';
import { css, StyleSheet } from 'aphrodite';

const styles = StyleSheet.create({
  sidebar: {
    display: 'flex',
    flexDirection: 'column',
    background: 'rgb(38,28,37)',
  },

  link: {
    position: 'relative',
    display: 'flex',
    width: '65px',
    color: 'rgba(255,255,255,.6)',
    ':hover': {
      textDecoration: 'none',
    },
    ':focus': {
      textDecoration: 'none',
    },
  },

  activeLink: {
    color: '#fff',
    ':after': {
      position: 'absolute',
      top: '12px',
      bottom: '12px',
      left: '0',
      width: '3px',
      background: 'rgba(255,255,255,.2)',
      borderTopRightRadius: '3px',
      borderBottomRightRadius: '3px',
      content: '""',
    },
  },

  badge: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    width: '45px',
    height: '45px',
    margin: '12px auto',
    fontSize: '20px',
    background: 'rgba(255,255,255,.2)',
    borderRadius: '5px',
  },

  logoutButton: {
    padding: '0',
    background: 'transparent',
    border: '0',
    cursor: 'pointer',
  },
});

type Child = {
  id: number,
  name: string,
}

type ChildLinkProps = {
  child: Child
}

const ChildLink = ({ child }: ChildLinkProps) =>
  <Link to={`/r/${child.id}`} className={css(styles.link)} activeClassName={css(styles.activeLink)}>
    <div className={css(styles.badge)}>
      <span>{child.name.charAt(0)}</span>
    </div>
  </Link>;

type Props = {
  chilren: Array<Child>,
  router: Object,
  onLogoutClick: () => void,
}

const Sidebar = ({ children, router, onLogoutClick }: Props) =>
  <div className={css(styles.sidebar)}>
    {children.map(child => <ChildLink key={child.id} child={child} />)}
    <Link
      to="/"
      activeOnlyWhenExact
      className={css(styles.link)}
      activeClassName={css(styles.activeLink)}
    >
      <div className={css(styles.badge)}>
        <span className="fa fa-plus" />
      </div>
    </Link>
    <div style={{ flex: '1' }} />
    <button
      onClick={() => onLogoutClick(router)}
      className={css(styles.link, styles.logoutButton)}
    >
      <div className={css(styles.badge)}>
        <span className="fa fa-sign-out" />
      </div>
    </button>
  </div>;

export default Sidebar;
