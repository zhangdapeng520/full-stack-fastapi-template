import React from 'react';
import { Container, Heading, Stack, Box, Button, HStack } from "@chakra-ui/react"
import { useTheme } from "next-themes"
import { useTranslation } from 'react-i18next';

import { Radio, RadioGroup } from "@/components/ui/radio"

const Appearance: React.FC = () => {
  const { theme, setTheme } = useTheme()
  const { t, i18n } = useTranslation();

  return (
    <Box p={6} boxShadow="md" borderRadius="md">
      <Heading mb={4}>{t('Appearance')}</Heading>
      <HStack spacing={4} mb={4}>
        <Button onClick={() => i18n.changeLanguage('zh')} colorScheme={i18n.language === 'zh' ? 'blue' : 'gray'}>
          中文
        </Button>
        <Button onClick={() => i18n.changeLanguage('en')} colorScheme={i18n.language === 'en' ? 'blue' : 'gray'}>
          English
        </Button>
      </HStack>
      <Container maxW="full">
        <Heading size="sm" py={4}>
          Appearance
        </Heading>

        <RadioGroup
          onValueChange={(e) => setTheme(e.value)}
          value={theme}
          colorPalette="teal"
        >
          <Stack>
            <Radio value="system">System</Radio>
            <Radio value="light">Light Mode</Radio>
            <Radio value="dark">Dark Mode</Radio>
          </Stack>
        </RadioGroup>
      </Container>
    </Box>
  )
}
export default Appearance
