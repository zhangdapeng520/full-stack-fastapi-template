import React from "react";
import { Menu, MenuButton, MenuList, MenuItem, Button } from "@chakra-ui/react";
import { ChevronDownIcon } from "@chakra-ui/icons";
import { useTranslation } from 'react-i18next';

const UserMenu: React.FC = () => {
  const { t } = useTranslation();
  return (
    <Menu>
      <MenuButton as={Button} rightIcon={<ChevronDownIcon />}>
        {t('User Settings')}
      </MenuButton>
      <MenuList>
        <MenuItem>{t('Change Password')}</MenuItem>
        <MenuItem>{t('Delete Account')}</MenuItem>
        <MenuItem>{t('Logout')}</MenuItem>
      </MenuList>
    </Menu>
  );
};

export default UserMenu;
