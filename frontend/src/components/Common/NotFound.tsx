import React from 'react';
import { Box, Heading, Text, Button } from '@chakra-ui/react';
import { Link } from '@tanstack/react-router';
import { useTranslation } from 'react-i18next';

const NotFound: React.FC = () => {
  const { t } = useTranslation();
  return (
    <Box textAlign="center" py={10} px={6}>
      <Heading display="inline-block" as="h2" size="2xl" bgGradient="linear(to-r, teal.400, teal.600)" backgroundClip="text">
        404
      </Heading>
      <Text fontSize="18px" mt={3} mb={2}>{t('Not Found')}</Text>
      <Text color={'gray.500'} mb={6}>
        {t('The page you are looking for does not seem to exist.')}
      </Text>
      <Button as={Link} to="/" colorScheme="teal" variant="solid">
        {t('Go to Home')}
      </Button>
    </Box>
  );
};

export default NotFound;
