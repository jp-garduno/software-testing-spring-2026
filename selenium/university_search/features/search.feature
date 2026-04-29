Feature: University search validation

  Scenario Outline: Search university and validate careers info
    Given I am on Google homepage
    When I search for "<universidad>"
    And I click the first result
    Then the page should contain "<dominio>"
    When I search for "<universidad> carreras" 
    Then results should contain "<resultado>"

    Examples:
      | universidad        | dominio   | resultado    |
      | iteso universidad  | iteso.mx  | ingeniería   |
      | udg universidad    | udg.mx    | licenciatura |
      | tec monterrey      | tec.mx    | carrera      |