import React from 'react';
import { Box, Button, Container, Heading, VStack, FormControl, FormLabel, Input } from "@chakra-ui/react"
import { useMutation } from "@tanstack/react-query"
import { type SubmitHandler, useForm } from "react-hook-form"
import { FiLock } from "react-icons/fi"
import { useTranslation } from 'react-i18next';

import { type ApiError, type UpdatePassword, UsersService } from "@/client"
import useCustomToast from "@/hooks/useCustomToast"
import { confirmPasswordRules, handleError, passwordRules } from "@/utils"
import { PasswordInput } from "../ui/password-input"

interface UpdatePasswordForm extends UpdatePassword {
  confirm_password: string
}

const ChangePassword: React.FC = () => {
  const { t } = useTranslation();
  const { showSuccessToast } = useCustomToast()
  const {
    register,
    handleSubmit,
    reset,
    getValues,
    formState: { errors, isValid, isSubmitting },
  } = useForm<UpdatePasswordForm>({
    mode: "onBlur",
    criteriaMode: "all",
  })

  const mutation = useMutation({
    mutationFn: (data: UpdatePassword) =>
      UsersService.updatePasswordMe({ requestBody: data }),
    onSuccess: () => {
      showSuccessToast("Password updated successfully.")
      reset()
    },
    onError: (err: ApiError) => {
      handleError(err)
    },
  })

  const onSubmit: SubmitHandler<UpdatePasswordForm> = async (data) => {
    mutation.mutate(data)
  }

  return (
    <Box p={6} boxShadow="md" borderRadius="md">
      <Heading mb={4}>{t('Change Password')}</Heading>
      <form onSubmit={handleSubmit(onSubmit)}>
        <VStack gap={4} w={{ base: "100%", md: "sm" }}>
          <FormControl mb={4}>
            <FormLabel>{t('Current Password')}</FormLabel>
            <PasswordInput
              type="current_password"
              startElement={<FiLock />}
              {...register("current_password", passwordRules())}
              placeholder={t('Current Password')}
              errors={errors}
            />
          </FormControl>
          <FormControl mb={4}>
            <FormLabel>{t('New Password')}</FormLabel>
            <PasswordInput
              type="new_password"
              startElement={<FiLock />}
              {...register("new_password", passwordRules())}
              placeholder={t('New Password')}
              errors={errors}
            />
          </FormControl>
          <FormControl mb={4}>
            <FormLabel>{t('Confirm Password')}</FormLabel>
            <PasswordInput
              type="confirm_password"
              startElement={<FiLock />}
              {...register("confirm_password", confirmPasswordRules(getValues))}
              placeholder={t('Confirm Password')}
              errors={errors}
            />
          </FormControl>
        </VStack>
        <Button
          variant="solid"
          mt={4}
          type="submit"
          loading={isSubmitting}
          disabled={!isValid}
        >
          {t('Submit')}
        </Button>
      </form>
    </Box>
  )
}

export default ChangePassword
