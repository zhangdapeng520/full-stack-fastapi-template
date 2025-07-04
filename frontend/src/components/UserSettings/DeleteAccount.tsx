import React from 'react';
import { Container, Heading, Text, Button } from "@chakra-ui/react"
import { useTranslation } from 'react-i18next';

import DeleteConfirmation from "./DeleteConfirmation"

const DeleteAccount = () => {
  const { t } = useTranslation();
  return (
    <Container maxW="full">
      <Heading size="sm" py={4}>
        {t('Delete Account')}
      </Heading>
      <Text>
        {t('Permanently delete your data and everything associated with your account.')}
      </Text>
      <DeleteConfirmation />
      <Text mb={4}>{t('Are you sure you want to delete your account?')}</Text>
      <Button colorScheme="red" onClick={() => {}} mr={3}>
        {t('Delete Account')}
      </Button>
      <Button>{t('Cancel')}</Button>
    </Container>
  )
}
export default DeleteAccount
