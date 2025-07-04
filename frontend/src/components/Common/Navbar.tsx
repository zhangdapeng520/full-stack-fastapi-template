import React from "react";
import { Box, Flex, HStack, IconButton, useColorModeValue } from "@chakra-ui/react";
import { HamburgerIcon } from "@chakra-ui/icons";
import { useTranslation } from 'react-i18next';
import { Link } from "@tanstack/react-router";

import Logo from "/assets/images/fastapi-logo.svg"
import UserMenu from "./UserMenu"

interface NavbarProps {
  onOpen: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ onOpen }) => {
  const { t } = useTranslation();
  return (
    <Box bg={useColorModeValue("white", "gray.900")} px={4} boxShadow="md">
      <Flex h={16} alignItems={"center"} justifyContent={"space-between"}>
        <IconButton
          size="md"
          icon={<HamburgerIcon />}
          aria-label={t('Open Menu')}
          onClick={onOpen}
        />
        <HStack spacing={8} alignItems={"center"}>
          <Box fontWeight="bold">{t('Dashboard')}</Box>
        </HStack>
      </Flex>
    </Box>
  );
};
